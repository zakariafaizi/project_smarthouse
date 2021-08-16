
import "bootstrap/dist/css/bootstrap.min.css"
import axios from 'axios'
import React, { useState, useEffect } from 'react';



class main extends React.Component {


    
    constructor(props){
        super(props);

        this.verifyData = this.verifyData.bind(this)

        this.state = {

            participants:[],
            leng:''
        }

        
 
    }


  

    componentDidMount()  //on start
    {
        this.timerID = setInterval(
            () => this.verifyData(),
            5000
          );

       
        this.updateList()
       

    }   


 
    updateList()
    {
        axios.get('http://localhost:3039/getParticipants')
        .then((response) => {
            const data = response.data;
            console.log('response data');
            console.log(response.data);
            if(data.length > 0 )
            {
                this.setState({participants : data , leng:data.length})
                console.log('data received');
                console.log(data);
                
                
                
            }

        
        })
        .catch((error) =>
        {
            console.log(error)
        });
        
    }

    verifyData(){

        axios.get('http://localhost:3039/getParticipants')
        .then((response) => {
            const data = response.data;
            console.log('response data');
            console.log(response.data);
            if(data.length !== this.state.leng )
            {
                this.setState({participants : data , leng:data.length})
                console.log('data received');
                console.log(data);
            }
          
        
        })
        .catch((error) =>
        {
            console.log(error)
        });


      
    }

  
    componentWillUnmount() {
        clearInterval(this.timerID);
      }

     studentsList()
    {
     
        return this.state.participants.map(currentt => {
    
            return(
                    <tr className="row">
                    <td  className="col-lg-3 col-xs-3 col-3">{currentt.name}</td>
                    <td className="col-lg-3 col-sm-3 col-xs-3 col-3">{currentt.time}</td>
                    <td className="col-lg-3 col-sm-3 col-xs-3 col-3">{currentt.count}</td>
                    <td className="col-lg-3 col-xs-3 col-3" ><img style={{borderRadius:50+'px' , borderWidth : 7,borderStyle: 'solid',borderColor:currentt.color}}  width="100px" height="100px" src={process.env.PUBLIC_URL + '/Images/'+currentt.name+'.jpg'} /></td> 

 
                
                    </tr>

                )
               
            })

           

    }


  


  render(){



  return (
    <div className="container">
    
    <center><h3> Participants</h3> </center>

     

      <table className="table">

          <thead className="thead-light">

              <tr className="row">
                  <th className="col-xs-3 col-lg-3 col-3">Name</th>
                  <th className="col-xs-3 col-lg-3 col-sm-3 col-xs-3 col-3">Arrival</th>
                  <th className="col-xs-3 col-lg-3 col-sm-3 col-xs-3 col-3">Counter</th>
                  <th className="col-xs-3 col-lg-3 col-3">Image</th> 
        
              </tr>
          </thead>

       
       
          <tbody>
              {this.studentsList()}

          </tbody>
        
      </table>




    </div>
    )
  }
}

export default main;