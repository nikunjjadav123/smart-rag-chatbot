const axios = require("axios");

const documents = [];

exports.uploadDocument = (req, res) => {
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
};

// exports.approveDocument = async (req, res) => {
//     const docId = parseInt(req.params.id);
//     const doc = documents.find(d => d.id === docId);

//     if (!doc) {
//         return res.status(404).json({ message: "Document not found" });
//     }

//     doc.status = "approved";

//     await axios.post(`${process.env.PYTHON_RAG_SERVICE}/embed`, {
//         file_path: doc.path
//     });

//     res.json({
//         message: "Document approved & sent for embedding",
//         document: doc
//     });
// };
