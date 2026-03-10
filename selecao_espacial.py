from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterNumber,
                       QgsSpatialIndex,
                       QgsDistanceArea,
                       QgsProject)

class SelecaoPontosIsolados(QgsProcessingAlgorithm):
    # Definindo os nomes das "caixas" de entrada
    INPUT = 'INPUT'
    REFERENCE = 'REFERENCE'
    RADIUS = 'RADIUS'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return SelecaoPontosIsolados()

    def name(self):
        return 'selecaopontosisolados'

    def displayName(self):
        return self.tr('Selecionar Pontos Isolados (Métrico)')

    def group(self):
        return self.tr('Scripts de Automação')

    def groupId(self):
        return 'scripts_automacao'

    def initAlgorithm(self, config=None):
        # Aqui o QGIS cria a interface automaticamente
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT, 'Camada para Seleção (Pontos)'))
        self.addParameter(QgsProcessingParameterFeatureSource(self.REFERENCE, 'Camada de Referência'))
        self.addParameter(QgsProcessingParameterNumber(self.RADIUS, 'Raio de busca (em metros)', defaultValue=1.0))

    def processAlgorithm(self, parameters, context, feedback):
        # 1. Pegando as camadas e o raio
        layer_a = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        layer_b = self.parameterAsVectorLayer(parameters, self.REFERENCE, context)
        raio_metros = self.parameterAsDouble(parameters, self.RADIUS, context)

        # 2. Configurando a régua inteligente (Geodésica)
        calculadora = QgsDistanceArea()
        calculadora.setEllipsoid(QgsProject.instance().ellipsoid())
        calculadora.setSourceCrs(layer_a.crs(), QgsProject.instance().transformContext())

        # 3. Criando o Índice Espacial na Camada B (Velocidade)
        feedback.pushInfo('Criando índice espacial...')
        index = QgsSpatialIndex(layer_b.getFeatures())

        # 4. Lógica de seleção
        ids_isolados = []
        total = layer_a.featureCount()
        
        for i, feicao_a in enumerate(layer_a.getFeatures()):
            if feedback.isCanceled(): break # Permite cancelar o processo
            
            ponto_a = feicao_a.geometry().asPoint()
            # Filtro rápido (BBOX) - usando um valor pequeno em graus para o índice
            bbox = feicao_a.geometry().boundingBox()
            bbox.grow(0.001) 
            
            ids_candidatos = index.intersects(bbox)
            ponto_isolado = True
            
            for id_b in ids_candidatos:
                feicao_b = layer_b.getFeature(id_b)
                distancia = calculadora.measureLine(ponto_a, feicao_b.geometry().asPoint())
                
                if distancia <= raio_metros:
                    ponto_isolado = False
                    break
            
            if ponto_isolado:
                ids_isolados.append(feicao_a.id())
            
            feedback.setProgress(int(i/total*100))

        # 5. Aplicando a seleção na camada original
        layer_a.selectByIds(ids_isolados)
        
        return {'PONTOS_ISOLADOS': len(ids_isolados)}
