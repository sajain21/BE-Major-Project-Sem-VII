import { useState } from 'react';
import './styleSignup.css';
import httpClient from "../httpClient";

function Register(){
    const [fname, setFirstName] = useState();
    const [lname, setLastName] = useState();
    const [email, setEmail] = useState();
    const [mobNo, setPhoneNum] = useState();
    const [password, setPass] = useState();

    const signUpUser = async () => {
      console.log(fname, lname, email, mobNo, password);
      try{
        const resp = await httpClient.post("//localhost:5000/register", {fname, lname, email, mobNo, password,});
        window.location.href="/";
      } catch(error){
        if(error.response.status === 401){
          alert("Invalid credintials");
        }
      }
    }

    console.log(fname);
    console.log(lname);
    console.log(email);
    console.log(mobNo);
    console.log(password);
    return(
        <div className="container">
      <form>
        <div className="loginTitle">
          <h1>Signup</h1>
        </div>
        <div className="inputField">
          <input type="text" placeholder="First name" required onChange={(e) => {setFirstName(e.target.value)}}/>
        </div>
        <div className="inputField">
          <input type="text" placeholder="Last name" required onChange={(e) => {setLastName(e.target.value)}}/>
        </div>
        <div className="inputField">
          <input type="text" placeholder="Email" required onChange={(e) => {setEmail(e.target.value)}}/>
        </div>
        <div className="inputField">
          <input type="number" placeholder="Enter mobile no." required onChange={(e) => {setPhoneNum(e.target.value)}}/>
        </div>
        <div className="inputField">
          <input type="password" placeholder="Enter Password" required onChange={(e) => {setPass(e.target.value)}}/>
        </div>
        <div className="inputField">
          <button type="button" onClick={() => signUpUser()}>Signup</button>
        </div>
        <div className="fp">
          <label>Already have an account?</label>
          <a href=' '> Login</a>
        </div>
      </form>
    </div>
    );
}

export default Register;