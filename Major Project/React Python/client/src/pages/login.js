import { useState } from "react";
import "./style.css";
import httpClient from "../httpClient";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPass] = useState("");

  const loginuser = async () => {
    console.log(email, password);

  try {
    const resp = await httpClient.post("//localhost:5000/login", {email, password,});
    window.location.href="/";
  } catch(error){
    if(error.response.status === 401){
      alert("Invalid credintials");
    }
  }
    // console.log(resp.data)
  //   if(resp.status === 200){
  //     window.location.href = "/";
  //   }
  //   else if(resp.status === 401){
  //     console.log("Error: Wrong password");
  //   }
  }
  // console.log(email);
  // console.log(password);
  return (
    <div className="container">
      <form>
        <div className="loginTitle">
          <h1>Login</h1>
        </div>
        <div className="inputField">
          <input type="text" placeholder="Email" required onChange={(e) => {setEmail(e.target.value)}}/>
        </div>
        <div className="inputField">
          <input type="password" placeholder="Passwrod" required onChange={(e) => {setPass(e.target.value)}}/>
        </div>
        <div className="fp">
          <a href=" ">forgot password?</a>
        </div>
        <div className="inputField">
          <button type="button" onClick={() => loginuser()}>Login</button>
        </div>
        <div className="signupLink">
          <p>Don't have an account?<a href=' '> Signup</a></p>
        </div>
      </form>
    </div>
  );
}

export default Login;