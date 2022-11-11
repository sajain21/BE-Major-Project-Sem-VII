import React, { useState, useEffect } from "react";
import httpClient from "../httpClient";

function Home() {
  const [user, setUser] = useState();
  const logoutUser = async () => {
    const resp = await httpClient.post("//localhost:5000/logout");
    window.location.href = "/";
  }
  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get("//localhost:5000/@me");
        setUser(resp.data);
        // console.log(user);
      } catch (error) {
        console.log("Not authenticated");
      }
    })();
  });
  return (
    <div>
      <h1>Welcome to React webpage</h1>
      {user != null ? (
        <div>
          <h2>Logged In</h2>
          <h3>Id: {user.id}</h3>
          <h3>Email: {user.email}</h3>

          <button onClick={logoutUser} style={{width:"100px"}}>logout</button>
        </div>
      ) : (
        <div>
          <p>You are not logged in</p>
          <a href="/login">
            <button style={{ width: "100px" }}>Login</button>
          </a>
          <a href="/register">
            <button style={{ width: "100px", marginLeft: "100px" }}>
              Signup
            </button>
          </a>
        </div>
      )}
      {/* <div>
                <p>You are not logged in</p>
            <a href="/login"><button style={{width:'100px'}} >Login</button></a>
            <a href="/login"><button style={{width:'100px', marginLeft:'100px'}}>Signup</button></a>
            </div> */}
    </div>
  );
}

export default Home;
