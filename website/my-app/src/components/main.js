import "bootstrap/dist/css/bootstrap.min.css"
import axios from 'axios'
import React from 'react';
import './main.css';



class main extends React.Component {


    
    constructor(props){
        super(props);

        this.verifyData = this.verifyData.bind(this)
        this.resetData = this.resetData.bind(this)
        this.seeAll = this.seeAll.bind(this)
        this.Active = this.Active.bind(this)

        this.state = {
            all:[],
            participants:[],
            leng:'',
            clicked:''
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

            this.setState({participants : data , leng:data.length})
     
    
          
        
        })
        .catch((error) =>
        {
            console.log(error)
        });


      
    }


    resetData(){

        axios.post('http://localhost:3039/reset')
        .then((response) => {
       
            this.setState({participants : [], leng:'',clicked:0})

        
        })
        .catch((error) =>
        {
            console.log(error)
        });


      
    }

    seeAll(){

        axios.post('http://localhost:3039/all')
        .then((response) => {
            const data = response.data;
            this.setState({all : data , leng:data.length,clicked:1})

        
        })
        .catch((error) =>
        {
            console.log(error)
        });
    }
    Active()
    {
        this.setState({clicked:0});

    }



    componentWillUnmount() {
        clearInterval(this.timerID);
      }

     peopleList()
    {
     
        if(this.state.leng > 0 && this.state.clicked <1)
        {

            return this.state.participants.map(currentt => {
    
                return(
                    
                    <tr className="row">
                    <td  className="col-lg-3 col-sm-3 col-xs-3 col-3">{currentt.name}</td>
                    <td className="col-lg-2 col-sm-2 col-xs-2 col-2">{currentt.timein}</td>
                    <td className="col-lg-2 col-sm-2 col-xs-2 col-2">{currentt.timeout}</td>
                    <td className="col-lg-2 col-sm-2 col-xs-2 col-2">{currentt.count}</td>
                    <td className="col-lg-3 col-xs-3 col-3" ><img style={{borderRadius:50+'px' , borderWidth : 7,borderStyle: 'solid',borderColor:currentt.color}}  width="100px" height="100px" src={process.env.PUBLIC_URL + '/Images/'+currentt.name+'.jpg'} /></td> 

                    </tr>
               
                   
                    )
                   
                })

        }
        else if(this.state.clicked === 1)
        {
            return this.state.all.map(currentt => {
    
                return(
                    
                        <tr className="row">
                        <td  className="col-lg-3 col-sm-3 col-xs-3 col-3">{currentt.name}</td>
                        <td className="col-lg-2 col-sm-2 col-xs-2 col-2">{currentt.timein}</td>
                        <td className="col-lg-2 col-sm-2 col-xs-2 col-2">{currentt.timeout}</td>
                        <td className="col-lg-2 col-sm-2 col-xs-2 col-2">{currentt.count}</td>
                        <td className="col-lg-3 col-xs-3 col-3" ><img style={{borderRadius:50+'px' , borderWidth : 7,borderStyle: 'solid',borderColor:currentt.color}}  width="100px" height="100px" src={process.env.PUBLIC_URL + '/Images/'+currentt.name+'.jpg'} /></td> 
    
                        </tr>
                   
                    )
                   
                })
        }
        else
        {
            
            return(
                
                    <tr className="row">
                    <td className="col-lg-3 col-sm-3 col-xs-3 col-3">-</td>
                    <td className="col-lg-2 col-sm-2 col-xs-2 col-2">-</td>
                    <td className="col-lg-2 col-sm-2 col-xs-2 col-2">-</td>
                    <td className="col-lg-2 col-sm-2 col-xs-2 col-2">-</td>
                    <td className="col-lg-3 col-sm-3 col-xs-3 col-3">-</td> 

                    </tr>
            
                )
                   
                

        }
        

           

    }


  


  render(){



  return (
    <div className="container">
    
    <center><br></br><h3>  S M A R T  H O U S E </h3><br></br></center>
        

      <table className="table">

          <thead className="thead-light">

         
              <tr className="row">
                  <th className="col-lg-3 col-sm-3 col-xs-3 col-3">Name</th>
                  <th className="col-lg-2 col-sm-2 col-xs-2 col-2">Arrival</th>
                  <th className="col-lg-2 col-sm-2 col-xs-2 col-2">Departure</th>
                  <th className="col-lg-2 col-sm-2 col-xs-2 col-2">Counter</th>
                  <th className="col-lg-3 col-sm-3 col-xs-3 col-3">Image</th> 
        
              </tr>
          
          </thead>

       
       
          <tbody>
              {this.peopleList()}

          </tbody>

               

        
      </table>


    <center class="row">
        <button type="button" onClick={this.Active} class="btn btn-info col-xs-12 col-sm-12 col-md-4 col-12 col-xl-4" >Inside</button>
        <button type="button" onClick={this.resetData} class="btn btn-warning col-xs-12 col-sm-12 col-md-4 col-12 col-xl-4">Reset</button>
        <button type="button" onClick={this.seeAll} class="btn btn-info col-xs-12 col-sm-12 col-md-4 col-12 col-xl-4">See All</button>
    </center>

    <br></br>
    <br></br>
 
    </div>
    )
  }
}

export default main;