import styled from "styled-components"
import { StateContext } from "../App"
import { useContext, useState } from "react"
import Button from "../common/Button"


const getTags = (input_str) => {

}

const BottomRight = ({children}) => {
    
    return (
        <div style={{position: "relative", height: "4rem", marginTop:"auto"}}>
            <div style={{position: "absolute", bottom: "0", right: "0", padding: "10px"}}>
                {children}
            </div>
        </div>
    )

}

const ThemedInput = styled.textarea`
    width: 100%;
    background: transparent;
    color: black;
    font-weight: 500;
    border-radius: 8px;
    /* height: 10rem; */
`

const SearchView = () => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)
    const [inputState, setInputState] = useState({input: '', typing: false, timeout: 0})
    const [tagList, setTagList] = useState([]);
    const [canContinue, setCanContinue] = useState(false);

    const timeout_ms = 300
    const min_query_len = 100
    
    const onInputChanged = (e) => {
        setCanContinue(e.target.value.length >= min_query_len)
        if (inputState.timeout) {
            clearTimeout(inputState.timeout)
        }
        setInputState({
            input: e.target.value,
            typing: false,
            timeout: setTimeout(() => {
                fetch(`/api/get_keywords?${(new URLSearchParams({q: e.target.value})).toString()}`)
                .then((response) => response.json())
                .then(({ results }) => {
                    console.log(results)
                    if(results) {
                        setTagList(results);
                    }
                })
                .catch((err) => {
                    console.log(err);
                })
                .finally(

                )
            }, timeout_ms)
        })
    }

    const sendRequest = (text) => {
        fetch(`/api/get_disease_results?q=${encodeURIComponent(text)}`)
        .then((response) => response.json())
        .then(({ results }) => setResults(results))
        .catch((error) => console.log(error));
    }

    return (
        <div className="h-100">
            <div className="text-center p-4 d-flex gap-3 flex-column justify-content-between" style={{height: "90%", }}>
                <div>
                    Note: Longer inputs will yield better results.
                </div>
                <ThemedInput onChange={onInputChanged}/>
                <h4 className="fw-bold">Identified Symptoms</h4>
                <div className="d-flex flex-row flex-wrap column-gap-2 row-gap-4">
                    {tagList && tagList.map((data) => (<div key={data} className="ps-3 pe-3 pt-1 pd-3 fw-medium" style={{background: "#dddddd", borderRadius: "4px"}}>
                        {data}
                    </div>))}
                </div>
                <BottomRight>
                    <Button text="Continue" onClick={() => {
                        sendRequest(inputState.input);
                        setPage(2);
                    }}/>
                </BottomRight>
            </div>
            
        </div>
    )
}

export default SearchView