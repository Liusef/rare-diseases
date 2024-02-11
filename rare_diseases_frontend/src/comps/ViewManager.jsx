import { useContext, useEffect, useState } from "react"
import HomeView from "./HomeView"
import TopToolbar from "./TopToolbar"
import SearchView from "./SearchView"
import { StateContext } from "../App"
import ResultsView from "./ResultsView"

const ViewManager = ({ ctx, setBack, setTitle }) => {
    const {page, setPage, results, setResults, selected, setSelected} = useContext(StateContext)

    // page
    // 0 - Home
    // 1 - Searching
    // 2 - Showing Results

    return (
        <div className="vh-100">
            <TopToolbar className="overflow-hidden"/>
            <div className="w-100 h-100 overflow-y-scroll ">
                {page == 0 && <HomeView/>}
                {page == 1 && <SearchView/>}
                {page == 2 && <ResultsView/>}
            </div>
        </div>
    )
}

export default ViewManager 