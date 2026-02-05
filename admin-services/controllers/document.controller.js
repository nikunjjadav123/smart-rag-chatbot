const { producer } = require("../kafka/kafkaProducer");
const documents = [];

exports.uploadDocument = async (req, res) => {
    try {

        await producer.connect();

        await producer.send({
            topic: "pdf_uploaded",
            messages: [
                {
                    value: JSON.stringify({
                        filename: req.file.filename,
                        path: req.file.path
                    })
                }
            ]

        });

        await producer.disconnect();

        const doc = {
            id: documents.length + 1,
            filename: req.file.filename,
            path: req.file.path,
            status: "pending"
        };

        documents.push(doc);

        res.json({
            message: "Document uploaded successfully",
            document: doc
        });

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};
