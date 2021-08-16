const express = require('express');
const app = express();

const goose = require('mongoose');
const conn = goose.connection;

const cors = require('cors');
app.use(cors());


const bodyParser = require('body-parser');

const student= require('./model/modelPerson');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));



app.get('/getParticipants' , (req,res) =>
{
    student.find({count: {$gt: 0 }})

    .exec()
    .then(user => res.status(200).json(user));
});

app.post('/reset' , (req,res) =>
{
    student.updateMany({}, {$set: {count: "0" }})
    .then(user => res.status(200).json(user));
    console.log("reset")

 
});





goose.connect('mongodb+srv://zakariafaizi:projetpfc123@clusterpfc.efa6c.mongodb.net/FaceRecognition',{  useUnifiedTopology: true ,useNewUrlParser: true,dbName: "FaceRecognition" });


conn.once('open' , () =>
{
    console.log("connected to mongoDB");
});


app.listen(3039, ()=>{
    console.log("listening to 3039");
});