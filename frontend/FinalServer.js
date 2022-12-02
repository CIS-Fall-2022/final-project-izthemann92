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
    message: 'Welcome to EJS HW 3'
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
            console.log(response);
            console.log(response.data)
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

app.get('/flight_overview', (req, res) =>{
    axios.all([
        axios.get('http://127.0.0.1:5000/flights'),
        axios.get('http://127.0.0.1:5000/airports'),
        axios.get('http://127.0.0.1:5000/planes')
    ])
        .then(axios.spread((flight,airports,plane) => {
            var data = flight.data

            console.log(flight.data[0])
            console.log(airports.data[0])
            console.log(plane.data[0])

            res.render('pages/index', {
                data: data
            })
        }))
        .catch(error => console.log(error))
})



// start the express application on port 8080
    app.listen(port, () => console.log('Application started listening'))