import { StateContext } from "../App";
import { useContext, useEffect } from "react";
import dismiss from "../assets/close.svg"
import styled from "styled-components";
import Button from "../common/Button";

const Outer = styled.div`
    margin: 2rem;
    box-shadow: 6px 6px;
    border-radius: 8px;
    border: 2px black solid;
    background: #FFF;
    overflow: scroll;
`

const Inner = styled.div`
    

`

const TitleDiv = styled.div`
    font-weight: bold;
    font-size: 3rem;
    text-overflow: wrap;
    text-transform: uppercase;
    background: var(--RareSight-Gradient, linear-gradient(94deg, #30615B 4.51%, #018B42 102.88%));
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
`

const ButtonRow = styled.div`
    display: flex;
    align-items: flex-start;
    align-self: stretch;
    gap: 20px;
`

const RightButton = styled.div`
border-radius: 2px;
border: 2px solid #FFF;
background: var(--RareSight-Gradient, linear-gradient(94deg, #30615B 4.51%, #018B42 102.88%));
box-shadow: 4px 4px 0px 0px #000;
    `


const DiseaseInfo = () => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)

    const handleClose = () => setSelected(false)

    return (
        <Outer>
            <Inner>
    
                <div className="overflow-scroll p-5 position-relative">
                
                    <div className="position-absolute top-0 end-0 m-5 p-2" style={{cursor: "pointer"}} onClick={handleClose}>
                        <img src={dismiss}/>
                    </div>
                    <TitleDiv>
                        {selected.name}
                    </TitleDiv>
                    <ButtonRow>
                        <Button text="Save"/>
                        <a target="_blank" href={selected.url}><Button text="Learn more" color="#009846" textColor="#ffffff"></Button></a>
                    </ButtonRow>
                    <div className="fw-bold fs-3 text-uppercase mt-4 mb-2 ">
                        Possible Symptoms   
                    </div>
                    <div className="fw-medium">
                        {selected.symptom_text}
                    </div>
                    <div className="fw-bold fs-3 text-uppercase mt-5 mb-2">
                        Affected Individuals    
                    </div>
                    <div className="fw-medium">
                        {selected.affected_text}
                    </div>
                </div>
            </Inner>
        </Outer>
    )
}

export default DiseaseInfo