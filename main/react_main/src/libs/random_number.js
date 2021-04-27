function randomNumber(minimum, maximum){
    //return a random number between min and max
    return (Math.random() * (maximum - minimum + 1) );
}

export default randomNumber;