import { useState, useContext, createContext } from 'react'
import Warning from './comps/warning.jsx'
import Starter from './common/starter.jsx'
import ViewManager from './comps/ViewManager.jsx'
import "./style.css"
import styled from 'styled-components'
import sample from './assets/sample_output.js'
import DiseaseInfo from './comps/DiseaseInfo.jsx'
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
    const [selected, setSelected] = useState({
        name: "Defaulting so hard rn",
        url: "https://google.com/",
        affected_text: "Acquired aplastic anemia affects males and females in about equal numbers. Most cases affect older children, teenagers or young adults. The incidence of aplastic anemia in Europe and Israel is two new cases among 1 million people per year. The incidence rate is two or three times greater in Asia. The exact incidence rates exist for the United States is unknown although some sources say that approximately 500-1,000 new cases of aplastic anemia are diagnosed each year.",
        symptom_text: "The symptoms of acquired aplastic anemia occur as a consequence of the bone marrow failing to produce enough blood cells. Specific symptoms vary from case to case. Some individuals may have mild symptoms that remain stable for many years; others may have serious symptoms that can progress to life-threatening complications. Red and white blood cells and platelets are formed in the bone marrow. The cells are released into the bloodstream to travel throughout the body performing their specific functions. Red blood cells deliver oxygen to the body’s organs, white blood cells help in fighting infections, and platelets form clots to stop bleeding. A low level of circulating red blood cells is called anemia. A low level of white blood cells is known as leukopenia. A low level of platelets is known as thrombocytopenia. Individuals with anemia may experience tiredness, increased need for sleep, weakness, lightheadedness, dizziness, irritability, headaches, pale skin color, difficulty breathing, and cardiac symptoms like chest pain. Individuals with leukopenia have an increase in risk of contracting bacterial and fungal infections. Individuals with thrombocytopenia are more susceptible to bruising following minimal injury and to spontaneous bleeding from the gums and nose. Women may have increased menstrual blood loss. Symptoms are dependent on the severity of the anemia, leukopenia, and thrombocytopenia. Some individuals with acquired aplastic anemia also have another disorder at the same time, called paroxysmal nocturnal hemoglobinuria (PNH). Acquired aplastic and PNH have a close relationship that is not fully understood by researchers. It is believed that PNH arises in the setting of autoimmune acquired aplastic anemia and bone marrow failure. Individuals affected with acquired aplastic anemia are also at risk that it will evolve into another similar disorder known as myelodysplasia. In a minority of cases, acquired aplastic anemia may eventually develop leukemia. PNH is caused by an acquired genetic defect affecting the PIGA gene, limited to marrow stem cells. The PIGA gene mutations cause blood cells to become sensitive to increased destruction by complement, a blood immunity protein. About half patients with aplastic anemia have evidence of PNH at presentation, as detected by flow cytometry. Furthermore, patients who respond following immunosuppressive therapy may recover with PNH. There are a minority of MDS patients with hypoplastic or low cellularity bone marrow, as seen in acquired aplastic anemia. These conditions are often mistaken for each other, so whether one is transformed to another is uncertain. (For more information on these disorders, see the Related Disorders section of this report.)"
    });



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
                    <div className='col-7 vh-100' style={{background: "#E5FFCC"}}>
                        <DiseaseInfo/>
                    </div>
                </div>
            </div>
        </StateContext.Provider>
    )
}

export default App
