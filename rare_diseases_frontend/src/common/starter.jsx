import { useState } from 'react'
import viteLogo from '/vite_unused.svg'
import reactLogo from '../assets/logo.svg'
import styled from 'styled-components';


const Logo = styled.img`
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;

    &:hover {
        filter: drop-shadow(0 0 2em #646cffaa);
    }
`;



const Starter = () => {
    const [count, setCount] = useState(0)

    return (
        <div style={{display: "flex", flexDirection: "column", width: "100vw", alignItems: "center"}}>
            <div className='w-100 d-flex align-items-center justify-content-center '>
            <a href="https://vitejs.dev" target="_blank">
                <Logo src={viteLogo} alt="Vite logo" />
            </a>
            </div>
            <h1>Vite + React</h1>
            <div className="card">
            <button onClick={() => setCount((count) => count + 1)}>
                count is {count}
            </button>
            <p>
                Edit <code>src/App.jsx</code> and save to test HMR
            </p>
            </div>
            <p className="read-the-docs">
            Click on the Vite and React logos to learn more
            </p>
        </div>
    )
}

export default Starter;