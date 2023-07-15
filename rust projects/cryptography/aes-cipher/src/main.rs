mod utility;
mod constants;


fn main() {

    let (x, y, z) = utility::aesKeyGenerator(999);
    println!("the aes key is = {} / {}", x, x.len());
    println!("hex key is = {:?} / {}", y, y.len());
    println!("number of rounds = {}", z);
    println!("stacked hex key = {:?}", utility::stackBytes(y));
    println!("s-box @(8, 9) = {:?}", constants::sBox("90", "08"));
    println!("i-s_box @(8, 9) = {:?}", constants::inverseSubstitution("90", "08"));
    println!("round constants @11 = {:?}", constants::roundConstants(9));
    let (a, b) = utility::encodeDocument("hello ".to_string());
    let (c, d) = utility::encodeDocument("Lift off".to_string());
    println!("'{}' in binary = {} and in hex = {}", "hello ", a, b);
    println!("'{}' in binary = {} and in hex = {}", "Lift off", c, d);
    println!("grouped msg = {:?}", utility::partitionDocument(a, x.len().try_into().unwrap()));

}
