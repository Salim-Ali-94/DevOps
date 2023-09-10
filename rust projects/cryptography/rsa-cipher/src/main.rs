mod utility;


fn main() {

    // let msg = "Lift off";
    let (phi, n) = utility::rsaPublicKeyGenerator(100);
    println!("(phi, n) = ({}; {})", phi, n);

}
