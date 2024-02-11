import styled from "styled-components";
import { StateContext } from "../App";
import { useEffect, useContext } from "react";
import DiseaseCard from "./DiseaseCard";





const ResultsView = () => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)
    
    const display_max = 10

    const row_elems = []
    console.log(results)
        for (let i = 0; i < Math.min(display_max, results.length); ++i) {
            row_elems.push(
                <DiseaseCard data={results[i]}/>
            )
        }

    return (
        <div className="container">
            <div className="d-flex flex-column gap-1 w-100 mt-4 mb-lg-4">
                {row_elems}
                <div style={{height: '96px'}}>

                </div>
            </div>
        </div>
    )
}

export default ResultsView

