const mongoose = require('mongoose');

const modelS = new mongoose.Schema({
    name: String,
    time: String,
    count: String,
    color: String

},{collection:'project'});

module.exports = mongoose.model('project' , modelS,'project');
