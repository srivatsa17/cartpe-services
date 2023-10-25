const throwAuthenticationErrorResponse = (error) => {
    if(error.response === null || error.response === undefined) {
        return "Oops! Something went wrong!";
    }

    if(!error.response.data.detail) {
        return error.message;
    }

    return error.response.data.detail
}

export default throwAuthenticationErrorResponse