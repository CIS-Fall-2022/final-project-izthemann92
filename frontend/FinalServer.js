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
    res.render('pages/thanks.ejs', {body: req.body})
  })

app.get('/add_flight',function(req, res) {
    axios.all([
        axios.get('http://127.0.0.1:5000/airports'),
        axios.get('http://127.0.0.1:5000/planes')
    ])
        .then(axios.spread((airports, planes)=>{
            var airports = airports.data
            var planes = planes.data
            res.render('pages/add_flight',{
                airports: airports,
                planes:planes
            })

        }));

})

// add form takes the data from the form and puts it through flights add api
app.post('/addform',(req,res)=>{
    let data = req.body
    console.log(data)
    axios.post('http://127.0.0.1:5000/flights',data)
        .then((response)=>{
            console.log(response)
        })


    res.render('pages/thanks.ejs',{body: req.body})

})

// ---------------------------------------- crud ops for planes -------------------------------------------------

// create planes
app.get('/planes_page', (request, response) => response.render("pages/planes_page.ejs", {

}))

// /planes_view connection
app.get('/planes_view', (req, res) =>{
    axios.get('http://127.0.0.1:5000/planes')
        .then((response) => {
            let planes = response.data
            res.render('pages/planes_page',{
                planes: planes
            })
        })

})


// created api to query for the flights overview 'view' that i created on the database.


// navigates to the add plane form
app.get('/add_plane', function(req, res) {

    res.render('pages/add_plane', {
    });
});
// planes add form
app.post('/Paddform',(req,res)=> {
    let data = req.body

    axios.post('http://127.0.0.1:5000/planes', data)
        .then((response) => {
            res.render('pages/thanks')
        })
})



// /update view
app.get('/update_view', (req, res) =>{
    axios.get('http://127.0.0.1:5000/planes')
        .then((response) => {
            let planes = response.data

            res.render('pages/update_plane',{
                planes: planes
            })
        })
})
// takes user to a page where they see the overview and select plane to update
app.post('/up_form', function(req, res){
    let data = req.body
    let id = req.body.id
    console.log(data)
    axios.put('http://127.0.0.1:5000/planes?id='+ id,data)
        .then((response) =>{
        })
    res.render('pages/thanks.ejs')
})



// /delete connection
app.get('/delete_view', (req, res) =>{
    axios.get('http://127.0.0.1:5000/planes')
        .then((response) => {
            let planes = response.data

            res.render('pages/delete_plane',{
                planes: planes
            })
        })
})
app.post('/d_form', function(req, res){
   let selectedID = req.body.id
    console.log(selectedID)
    axios.delete('http://127.0.0.1:5000/planes?id='+ selectedID)
        .then((response)=>{
            console.log(response)
        })
    res.render('pages/thanks.ejs', {body: req.body})

  })

// ---------------------------------------- crud ops for airports -------------------------------------------------

app.get('/airport_page', (request, response) => response.render("pages/airports_page.ejs", {

}))

app.get('/airports_view', (req, res) =>{
    axios.get('http://127.0.0.1:5000/airports')
        .then((response) => {
            let airports = response.data
            console.log(airports)

            res.render('pages/airports_page',{
                airports: airports
            })
        })

})
app.get('/add_airport', function(req, res) {

    res.render('pages/add_airport', {
    });
});
// airports add form
app.post('/Aaddform',(req,res)=> {
    let data = req.body
    axios.post('http://127.0.0.1:5000/airports', data)
        .then((response) => {
            res.render('pages/thanks')
        })
})

app.get('/Aupdate_view', (req, res) =>{
    axios.get('http://127.0.0.1:5000/airports')
        .then((response) => {
            let airports = response.data

            res.render('pages/update_airport',{
                airports: airports
            })
        })
})
// takes user to a page where they see the overview and select plane to update
app.post('/Aup_form', function(req, res){
    let data = req.body
    let id = req.body.id
    console.log(data)
    axios.put('http://127.0.0.1:5000/airports?id='+ id,data)
        .then((response)=>{
            console.log(response)
        })

    res.render('pages/thanks.ejs')
})

app.get('/Adelete_view', (req, res) =>{
    axios.get('http://127.0.0.1:5000/airports')
        .then((response) => {
            let airports = response.data

            res.render('pages/delete_airport',{
                airports: airports
            })
        })
})
app.post('/Ad_form', function(req, res){
   let selectedID = req.body.id
    console.log(selectedID)
    axios.delete('http://127.0.0.1:5000/airports?id='+ selectedID)
        .then((response)=>{
            console.log(response)
        })
    res.render('pages/thanks.ejs', {body: req.body})

  })


// start the express application on port 8080
    app.listen(port, () => console.log('Application started listening'))