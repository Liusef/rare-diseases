import { useContext, useEffect, useState } from "react"
import HomeView from "./HomeView"
import TopToolbar from "./TopToolbar"
import SearchView from "./SearchView"
import { StateContext } from "../App"

const ViewManager = ({ ctx, setBack, setTitle }) => {
    const {page, setPage, state, setState} = useContext(StateContext)
    // page
    // 0 - Home
    // 1 - Searching
    // 2 - Loading results?
    // 3 - Showing Results

    return (
        <div className="vh-100">
            <TopToolbar/>
            <div className="w-100 h-100">
                {page == 0 && <HomeView/>}
                {page == 1 && <SearchView/>}
            </div>
        </div>
    )
}

export default ViewManager 