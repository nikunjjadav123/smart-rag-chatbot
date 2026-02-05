const { Kafka } = require("kafkajs");

const kafkaClient = new Kafka({
    clientId: "pdf-uploader",
    brokers: ["localhost:9092"],
});

const producer = kafkaClient.producer();

module.exports = { producer };
