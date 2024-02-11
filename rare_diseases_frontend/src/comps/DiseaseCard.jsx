import styled from "styled-components"
import { StateContext } from "../App"
import { useContext } from "react"

const Card = styled.div`
    display: flex;
    flex-direction: column;
    background: #eeeeee;
    border-radius: 8px;
    border: 2px black solid;
    padding: 6px;
`

const CardTitle = styled.div`
    
`

const CardUrl = styled.a`
    font-size: 0.75rem;
    padding: 0.1rem;
    background: #22ffaa22;
    border-radius: 2px;
    margin-right: auto;
    cursor: pointer;
`

const CardSymptoms = styled.div`
    text-overflow: ellipsis;
    height: 4rem;
    font-size: 0.75rem;
`

const DiseaseCard = ({data}) => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)

    console.log(data)

    const clickHandler = () => {
        setSelected(data)
        console.log(`set selected to ${selected}`)
    }

    return (
        <Card onClick={clickHandler}>
            <CardTitle>
                {data.name}
            </CardTitle>
            <CardUrl>
                {data.url}
            </CardUrl>
            <CardSymptoms>
                {data.symptom_text}
            </CardSymptoms>
        </Card>
    )
}

export default DiseaseCard