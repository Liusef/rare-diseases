import { useState, useContext, createContext } from 'react'
import Warning from './comps/warning.jsx'
import Starter from './common/starter.jsx'
import ViewManager from './comps/ViewManager.jsx'
import "./style.css"
import styled from 'styled-components'
import sample from './assets/sample_output.js'
import DiseaseInfo from './comps/DiseaseInfo.jsx'
import LogoView from './comps/LogoView.jsx'
import logo from "./assets/logo.svg"

export const StateContext = createContext()

const LeftDiv = styled.div.attrs({
    className: 'col-5 vh-100 border border-2 border-black'
})`
    background: #fff;
    box-sizing: border-box;  
`;

function App() {
    // const [modalShow, setModalShow] = useState(true);
    const [page, setPage] = useState(0);
    const [results, setResults] = useState(sample)
    const [selected, setSelected] = useState(0);



    console.log(page)
    console.log(selected)
    console.log(results)

    return (
        <StateContext.Provider value={{page: page, setPage: setPage, results: results, setResults: setResults, selected: selected, setSelected: setSelected}}>
            <Warning />
            <div className='vw-100 overflow-hidden'>
                <div className='row gx-0'>
                    <LeftDiv>
                        <ViewManager/>
                    </LeftDiv>
                    <div className='col-7 vh-100 overflow-y-scroll' style={{background: "#E5FFCC"}}>
                        {selected ? <DiseaseInfo/> : <LogoView/>}
                    </div>
                </div>
            </div>
        </StateContext.Provider>
    )
}

export default App
