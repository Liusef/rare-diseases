import logo from "../assets/logo.svg"

const LogoView = () => {
    return (
        <div className="d-flex h-100  flex-row align-items-center">
            <div className="d-flex w-100 flex-column align-items-center opacity-25 ">
                <img src={logo}/>
                <div className="h1 mt-3 fw-bold ">
                    RareSight
                </div>
            </div>
        </div>
    )
}

export default LogoView