import styled from "styled-components"
import { StateContext } from "../App"
import { useContext } from "react"

const ThemeInput = styled.input`
    width: 100%;
`

const SearchView = () => {
    const {page, setPage, state, setState} = useContext(StateContext)

    return (
        <div className="text-center m-4">
            <ThemeInput/>
        </div>
    )
}

export default SearchView