const express = require('express');
const app = express();
const bodyParser = require('body-parser');

const axios = require('axios');
const path = require("path");
const {get, request} = require("axios");
const res = require("express/lib/response");
const {response} = require("express");

app.use(bodyParser.urlencoded());

const port = 8080

app.set("views", path.resolve(__dirname, "views"))
app.set("view engine", "ejs");

app.get('/', (request, response) => response.render("pages/login", {

}))

app.post('/process_login', async function (req, res) {
    var usr = req.body.username;
    var pwd = req.body.password;
    const url ='http://127.0.0.1:5000/login';
    // creating a way to insert the user data from form and posting to headers
    const options ={
        headers: {'username': usr,
                    'password': pwd}
    }
    axios.post(url, {}, options)
        .then((response) => {
            if (response.data === 'COULD NOT VERIFY!')
                res.render('pages/login',{
                    user: 'UNAUTHORIZED',
                    auth: false
                })
            else
                res.render('pages/home',{
                    user: usr,
                    auth: true
                })
        }, (error) => {
            console.log(error);
        })
})
// created api to query for the flights overview 'view' that i created on the database.
app.get('/flight_overview', (req, res) =>{
    axios.get('http://127.0.0.1:5000/flight_o')
        .then((response) => {
            let flights = response.data

            res.render('pages/index',{
                flights: flights
            })
        })
})
// created process dynamic form to delete the selected flight
app.post('/processdynamicform', function(req, res){
    selectedID = req.body
      for (x in req.body) {
        var selectedName = x;
        axios.delete('http://127.0.0.1:5000/flights?id='+ selectedName)
    }
    res.render('pages/index', {body: req.body})
  })

app.get('/add_flight',function(req, res) {
    axios.get('http://127.0.0.1:5000/airports')
        .then((response) => {
            let airports = response.data
            console.log(airports)
            res.render('pages/add_flight',{
                airports: airports
            });

        });

})


app.post('/add',(req,res)=>{
    axios.all([

    ])

})

// start the express application on port 8080
    app.listen(port, () => console.log('Application started listening'))