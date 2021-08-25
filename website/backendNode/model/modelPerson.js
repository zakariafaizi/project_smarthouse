const mongoose = require('mongoose');

const modelS = new mongoose.Schema({
    name: String,
    count: String,
    color: String,
    timein:String,
    timeout:String

},{collection:'project'});

module.exports = mongoose.model('project' , modelS,'project');
