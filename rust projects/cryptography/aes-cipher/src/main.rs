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
    // println!("i-s_box @(8, 9) = {:?}", *constants::inverseSubstitution.get(&("2", "0"))).unwrap();
    println!("round constants @11 = {:?}", constants::roundConstants(11));

}
