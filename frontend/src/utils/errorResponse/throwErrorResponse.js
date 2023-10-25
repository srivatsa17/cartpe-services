const throwErrorResponse = (error) => {
    if(error.response === null || error.response === undefined) {
        return "Oops! Something went wrong!";
    }

    if(!error.response.data.message) {
        return error.message;
    }

    return error.response.data.message
}

export default throwErrorResponse