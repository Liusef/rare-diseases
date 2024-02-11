import Button from "../common/Button"
import styled from "styled-components"
import {useContext, useEffect} from "react";
import { StateContext } from "../App"

const RSStyle = styled.div`
    font-weight: 800;
    font-size: 4rem;
    // color: #009846;
    /* filter: drop-shadow(0 0 64px #02e29faa); */
    background: var(--RareSight-Gradient, linear-gradient(94deg, #30615B 4.51%, #018B42 102.88%));
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
`

const HomeView = ({ ctx }) => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)

    return (
        <div className="h-100 d-flex flex-row align-items-center">

            <div className="w-100 d-flex flex-column align-items-center">
                    <RSStyle>
                        RareSight
                    </RSStyle>
                    <div className="text-center fs-5 fw-bolder text-uppercase ">
                        <div>
                            Enter symptoms.
                        </div>
                        <div style={{marginTop: "-0.5rem", marginBottom: "1rem"}}>
                            Explore rare diseases.
                        </div>
                    </div>
                    <Button text="Get Started" onClick={() => setPage(1)}/>
                    <div style={{height: "100px"}}>
                        {/* Just to move the home stuff up a bit */}
                    </div>
            </div>

        </div>
    )
}

export default HomeView