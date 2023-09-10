mod utility;

fn main() {

    let msg = "Lift off";
    // let (e, n) = utility::rsaKeyGenerator();
    let (e, n) = utility::rsaKeyGenerator(100);
    println!("(e, n) = ({}; {})", e, n);

}
