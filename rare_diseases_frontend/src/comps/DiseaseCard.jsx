import styled from "styled-components"
import { StateContext } from "../App"
import { useContext } from "react"
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const Card = styled.div`
    display: flex;
    width: 600;
    padding: 15px 30px;
    align-items: flex-start;
    gap: 100px;
    border-radius: 10px;
    border: 2px solid var(--Stroke, #000);
    background: #FFF;
    /* Hard Shadow */
    box-shadow: 4px 4px 0px 0px #000;
    margin-bottom: 20px;
    transition: .1s;
    cursor: pointer;

    &:hover {
        transform: translate(4px, 4px);
        transition: .1s;
        box-shadow: 0px 0px 0px 0px black;
    }

    &:active {
        background: #DDDDDD;
      }
`
const CardLeft = styled.div`
  display: flex;
  width: 300px;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  flex-shrink: 0;
`

const CardRight = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
`

const CardTitle = styled.div`
color: var(--Raresight-Teal, #1A7650);
text-transform: uppercase;
/* Card Header */
/* font-family: "Avenir Next"; */
font-size: 16px;
font-style: normal;
font-weight: 700;
line-height: normal;
`

const CardSubtitle = styled.div`
color: #000;
/* font-family: "Avenir Next"; */
font-size: 14px;
font-style: italic;
font-weight: 400;
line-height: normal;`

const CardBody = styled.div`
color: #000;
/* font-family: "Avenir Next"; */
font-size: 12px;
font-style: normal;
font-weight: 400;
line-height: normal;`

const CardFooter = styled.div`
color: #000;
/* font-family: "Avenir Next"; */
font-size: 12px;
font-style: normal;
font-weight: 400;
line-height: normal;
`
function getFirstSentence(text) {
    const match = text.match(/^[^.!?]+[.!?]/);
    return match ? match[0] : text;
  }

const DiseaseCard = ({data}) => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)

    console.log(data)

    const percentage = data.probability ? (data.probability * 100) : 0

    const clickHandler = () => {
        setSelected(data)
        console.log(`set selected to ${selected}`)
    }

    let body_text = getFirstSentence(data.symptom_text)

    return (
        <Card onClick={clickHandler}>
            <CardLeft>
                <CardTitle>
                    {data.name}
                </CardTitle>
                <CardSubtitle>
                    {data.url}
                </CardSubtitle>
                <CardBody>
                    {body_text}
                </CardBody>
            </CardLeft>
            <CardRight>
              <CircularProgressbar value={percentage} text={`${Math.round(percentage)}%`} styles={buildStyles({
                pathColor: `#009846`,
                textColor: 'black',
                trailColor: 'transparent',
              })}/>
              <div>
                Relevance
              </div>
            </CardRight>
            
        </Card>
    )
}

export default DiseaseCard