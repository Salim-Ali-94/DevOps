mod utility;


fn main() {

    let (x, y, z) = utility::aesKeyGenerator(999);
    println!("the aes key is = {} / {}", x, x.len());
    println!("hex key is = {:?} / {}", y, y.len());
    println!("number of rounds = {}", z);
    println!("stacked hex key = {:?}", utility::stackBytes(y));
    println!("s-box @(8, 9) = {:?}", utility::constants::sBox("90", "08"));
    println!("i-s_box @(8, 9) = {:?}", utility::constants::inverseSubstitution("90", "08"));
    println!("round constants @11 = {:?}", utility::constants::roundConstants(9));
    let (a, b) = utility::encodeDocument("hello ".to_string());
    let (c, d) = utility::encodeDocument("Lift off! bro what, huh yeah, just beat it!????".to_string());
    println!("'{}' in binary = {} and in hex = {}", "hello ", a, b);
    println!("'{}' in binary = {} / {} and in hex = {}", "Lift off! bro what, huh yeah, just beat it!????", c, c.len(), d);
    let e = utility::partitionDocument(c, x.len().try_into().unwrap());
    let f = utility::partitionMessage(d, x.len().try_into().unwrap());
    println!("grouped msg = {:?}", e);
    println!("grouped hex msg = {:?}", f);
    // println!("grouped msg = {:?}", utility::partitionDocument(c, x.len().try_into().unwrap()));
    // println!("grouped hex msg = {:?}", utility::partitionMessage(d, x.len().try_into().unwrap()));
    // println!("shuffled first word = {:?}", utility::shuffleVector(utility::partitionDocument(c, x.len().try_into().unwrap())[0][0].clone()));

    // println!("shuffled first word = {:?}", utility::shuffleVector(e[0][0].clone()));
    println!("shuffled hex first word = {:?}", utility::shuffleVector(f[0][0].clone()));
    let (row, col) = utility::formatIndex(f[0][0][0].clone());
    println!("aes sub row / column = {} / {}", row, col);
    println!("corresponding aes sub = {}", utility::constants::sBox(&row, &col));
    // println!("shuffled first word = {:?}", utility::partitionDocument(c, x.len().try_into().unwrap())[0]);
    // println!("shuffled first word deeper = {:?}", utility::partitionDocument(c, x.len().try_into().unwrap())[0][0]);

}
