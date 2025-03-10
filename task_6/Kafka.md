### *Развернуть Kafka, используя официальный GET STARTED (JAR-архив)*

1. Скачал tar архив kafka с официального репозитория: 
   `wget https://downloads.apache.org/kafka/3.8.1/kafka_2.13-3.8.1.tgz`
2. Далее запустил:
	- ZooKeeperServer со стандартной конфигурацией `bin/zookeeper-server-start.sh config/zookeeper.properties`
	- Kafka Server `bin/kafka-server-start.sh config/server.properties`
		> [!Quote]
		> Установил в конфигурации *server.properties* ip ВМ: 192.168.157.141 для корректной работы с *kafka-ui* 
3. Установил Docker и Docker compose для упрощения процесса развертывания Kafka-ui. Собрал docker-compose.yaml с необходимыми параметрами для запуска:
```
services:
  kafka-ui:
    image: provectuslabs/kafka-ui
    container_name: kafka-ui
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: "local"
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: "192.168.157.141:9092"
```

Поднял kafka ui с помощью `docker compose up -d`

4. Создал топик с именем topic через ui
5. Создал producer: `bin/kafka-console-producer.sh --topic topic --bootstrap-server localhost:9092`
6. Создал Consumer: `bin/kafka-console-consumer.sh --topic topic --from-beginning --bootstrap-server localhost:9092`
7. Обменялся сообщениями через topic между ними.