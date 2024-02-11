import { StateContext } from "../App";
import { useContext, useEffect } from "react";



const DiseaseInfo = () => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)

    return (
        <div className="overflow-scroll">
            <div>
                {selected.name}
            </div>
            <div>
                {selected.url}
            </div>
            <div>
                {selected.affected_text}
            </div>
            <div>
                {selected.symptom_text}
            </div>
            
        </div>
    )
}

export default DiseaseInfo