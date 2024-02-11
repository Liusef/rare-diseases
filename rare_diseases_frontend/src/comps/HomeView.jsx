import Button from "../common/Button"
import styled from "styled-components"
import {useContext, useEffect} from "react";
import { StateContext } from "../App"

const RSStyle = styled.div`
    font-weight: bold;
    font-size: 3rem;
`

const HomeView = ({ ctx }) => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)

    useEffect(() => {
        fetch('/api/get_keywords?q=adhd')
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
                    <Button text="Get Started" onClick={() => setPage(1)}/>
                    <div style={{height: "100px"}}>
                        {/* Just to move the home stuff up a bit */}
                    </div>
            </div>

        </div>
    )
}

export default HomeView