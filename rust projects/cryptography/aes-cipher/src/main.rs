mod utility;


fn main() {

    utility::aesKeyGenerator(-1);
    utility::aesKeyGenerator(150);
    let (x, y) = utility::aesKeyGenerator(999);
    println!("key length is = {}", x);
    println!("number of rounds = {}", y);

}
