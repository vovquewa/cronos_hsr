from qEngineApi import QlikEngine
import json
import logging
from logging.handlers import RotatingFileHandler


# подключение .env
from dotenv import load_dotenv
import os

# получаем переменную пути проекта
from definitions import PROJECT_PATH


def json_parser(json_data):
    result = []
    for i in json_data:
        result.append({
            "operator": i[0]['qText'],
            "sales": i[1]['qText'],
            "return": i[2]['qText'],
            "payment": i[3]['qText'],
            "date": i[4]['qText'],
        })
    return result


def main():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    filename = os.path.basename(__file__).split('.')[0]
    handler = RotatingFileHandler(
        f'{PROJECT_PATH}/logs/{filename}.log', maxBytes=500000
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    load_dotenv()
    QLIK_HOST = os.getenv('QLIK_HOST')
    QLIK_USER_DIRECTORY = os.getenv('QLIK_USER_DIRECTORY')
    QLIK_USER_ID = os.getenv('QLIK_USER_ID')
    QLIK_CERT_PATH = os.path.join(PROJECT_PATH, os.getenv('QLIK_CERT_PATH'))
    QLIK_DOC_ID_OUTBOUND = os.getenv('QLIK_DOC_ID_OUTBOUND')
    QLIK_DOC_OBJECT_OUTBOUND = os.getenv('QLIK_DOC_OBJECT_OUTBOUND')

    engineConnect = QlikEngine(
        host=QLIK_HOST,
        cert_path=QLIK_CERT_PATH,
        user_directory=QLIK_USER_DIRECTORY,
        user_id=QLIK_USER_ID,
    )

    # создаем сессию
    sessionCreated = engineConnect.sessionCreated

    if sessionCreated:
        logger.info('Сессия создана')
        # открываем документ
        doc = engineConnect.openDoc(QLIK_DOC_ID_OUTBOUND)
        # получаем хэндл документа
        docHandle = doc['result']['qReturn']['qHandle']
        # получаем объект
        object = engineConnect.getObject(docHandle, QLIK_DOC_OBJECT_OUTBOUND)
        # получаем хэндл объекта
        objectHandle = object['result']['qReturn']['qHandle']
        # получаем данные из гиперкуба
        request = {
            "handle": objectHandle,
            "method": "GetHyperCubeData",
            "params": {
                "qPath": "/qHyperCubeDef",
                "qPages": [
                    {
                        "qLeft": 0,
                        "qTop": 100,
                        # органичение qlik api: max(qWidth * qHeight) == 10000
                        "qWidth": 5,
                        "qHeight": 4
                    }
                ]
            }
        }

        result = json_parser(engineConnect.sendRequest(
            request
        )["result"]["qDataPages"][0]["qMatrix"])

        # result = engineConnect.sendRequest(
        #     request
        # )["result"]["qDataPages"][0]["qArea"]

        print(json.dumps(result, indent=4))
        logger.info('Ответ гиперкуба успешно распарсен')

        # убиваем сессию после того как завершили все действия
        del engineConnect
    else:
        logger.error('Сессия не была создана')


if __name__ == '__main__':
    main()
