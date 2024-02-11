import styled from "styled-components"
import LeftArrow from"/left_arrow.svg" 
import { useContext, useEffect, useState } from "react";
import { StateContext } from "../App";


const toolbar_height = "4rem"

const Toolbar = styled.div`
    border-radius: 0px 0px 10px 0px;
    outline: 2px solid var(--Stroke, #000);
    background: #FFF;
    height: ${toolbar_height};
    position: relative;

    
    /* display: flex;
    justify-content: space-between;
    align-items: center; */
`;


const LeftParent = styled.div`
    position: absolute;
    top: 0;
    height: 100%;

`

const LeftChild = styled.div`
    height: 100%;
    padding: 10px;
    display: flex;
    flex-direction: row;
    align-items: center;
`

const BackButton = styled.img`
    fill: black;
`

const TopToolbar = () => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)
    const [title, setTitle] = useState("RareSight")
    const [showBack, setShowBack] = useState(false)
    
    useEffect(() => {
        if (page == 1) {
            setTitle("Enter Symptoms")
        } else if (page == 2) {
            setTitle(`Found ${results.length} result${results.length != 1 ? "s" : ""}`)
        } else {
            setTitle("Welcome to RareSight")
        }
    },[page, results])

    return (
        <Toolbar>
            <div className="w-100 h-100 d-flex flex-column align-items-center">
                <div className="d-flex flex-row align-items-center fw-bold fs-5 text-uppercase" style={{height: toolbar_height}}>
                    {title}
                </div>
            </div>
            <LeftParent>
                <LeftChild>
                    {
                        page > 0 && <BackButton src={LeftArrow} onClick={() => setPage(page - 1)} style={{cursor: "pointer"}}/> 
                    }
                </LeftChild>
            </LeftParent>
        </Toolbar>
    )
}

export default TopToolbar