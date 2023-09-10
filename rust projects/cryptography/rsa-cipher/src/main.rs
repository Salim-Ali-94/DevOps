mod utility;


fn main() {

    // let msg = "Lift off";
    let (p, q, n, phi, e) = utility::rsaPublicKeyGenerator(100);
    println!("(p, q, n, phi, e) = ({}; {}; {}; {}; {})", p, q, n, phi, e);

}
