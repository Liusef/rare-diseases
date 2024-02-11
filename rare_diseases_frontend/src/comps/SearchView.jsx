import styled from "styled-components"
import { StateContext } from "../App"
import { useContext, useState } from "react"
import Button from "../common/Button"


const getTags = (input_str) => {

}

const BottomRight = ({children}) => {
    
    return (
        <div style={{position: "relative", height: "100%"}}>
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
    /* height: 5rem; */
`

const SearchView = () => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)
    const [inputState, setInputState] = useState({input: '', typing: false, timeout: 0})
    const [tagList, setTagList] = useState([])
    const [canContinue, setCanContinue] = useState(false)
    
    const timeout_ms = 3000
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
                fetch(`http://143.215.127.46:5000/get_possible_keywords?q=${e.target.value}`)
                .then((resp) => setTagList(resp[results]))
                .catch((err) => {
                    console.log(err)
                    setTagList([])
                })
                .finally(

                )
            }, timeout_ms)
        })
    }

    const sendRequest = (text) => {

        

    }

    return (
        <div className="h-100">
            <div className="text-center m-4" style={{height: "74%"}}>
                <div>
                    Input must be at least {min_query_len} characters.
                </div>
                <ThemedInput onChange={onInputChanged}/>
                <div>
                    {tagList}
                </div>
                <BottomRight>
                    <Button text="Continue" onClick={() => {
                        const ret = sendRequest(inputState.input)
                        // setResults(ret)
                        setPage(2)
                    }}/>
                </BottomRight>
            </div>
            
        </div>
    )
}

export default SearchView