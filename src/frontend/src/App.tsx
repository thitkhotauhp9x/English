import {useState, type SetStateAction} from "react";


function App() {
  const [text, setText] = useState('');

  function handleClick() {
    console.log(text);
  }

  function handleChange(e: { target: { value: SetStateAction<string>; }; }) {
    setText(e.target.value);
  }

  return (
    <>
      <div>
        <label>Search</label>
        <input value={text} onChange={handleChange}></input>
        <br/>
        <button onClick={handleClick}>Submit</button>
        <br/>
        <div>
          Result
        </div>
      </div>
    </>
  )
}

export default App
