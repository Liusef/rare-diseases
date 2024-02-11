import { useState, useContext, createContext } from 'react'
import Warning from './comps/warning.jsx'
import Starter from './common/starter.jsx'
import ViewManager from './comps/ViewManager.jsx'
import "./style.css"
import styled from 'styled-components'

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
    const [state, setState] = useState({});

    console.log(page)
    console.log(state)

    return (
        <StateContext.Provider value={{page: page, setPage: setPage, state: state, setState: setState}}>
            <Warning />
            <div style={{width: "100vw"}}>
                <div className='row gx-0'>
                    <LeftDiv>
                        <ViewManager/>
                    </LeftDiv>
                    <div className='col-7 vh-100' style={{background: "#225599"}}>
                        urmom
                    </div>
                </div>
            </div>
        </StateContext.Provider>
    )
}

export default App
