import Button from "../lib/Button"
import styled from "styled-components"
import {useContext, useEffect} from "react";
import { StateContext } from "../App"

const RSStyle = styled.div`
    font-weight: bold;
    font-size: 3rem;
`

const HomeView = ({ ctx }) => {
    const {page, setPage, state, setState} = useContext(StateContext)

    useEffect(() => {
        fetch('http://143.215.127.46:5000')
        .then((resp) => console.log(resp))
        .catch((err) => console.log(err))
        .finally(() => console.log('loaded'));
    }, [])
    return (
        <div className="h-100 d-flex flex-row align-items-center">

            <div className="w-100 d-flex flex-column align-items-center">
                    <RSStyle>
                        RareSight
                    </RSStyle>
                    <div className="fs-3">
                        Enter symptoms.
                    </div>
                    <div className="fs-3" style={{marginTop: 0, marginBottom: "1rem"}}>
                        Explore rare diseases.
                    </div>
                    <Button text="Get Started" onClick={() => {
                        let temp = state 
                        temp.search_query = ""
                        temp.tags = []
                        setPage(1)
                    }}/>
                    <div style={{height: "100px"}}>
                        {/* Just to move the home stuff up a bit */}
                    </div>
            </div>

        </div>
    )
}

export default HomeView