mod utility;


fn main() {

    let (x, y, z) = utility::aesKeyGenerator(999);
    println!("the aes key is = {} / {}", x, x.len());
    println!("hex key is = {:?} / {}", y, y.len());
    println!("number of rounds = {}", z);
    println!("stacked hex key = {:?}", utility::stackBytes(y));
    println!("round constants @9 = {:?}", utility::constants::roundConstants.get(&9).unwrap());
    let (a, b) = utility::encodeDocument("hello ".to_string());
    let (c, d) = utility::encodeDocument("Lift off! bro what, huh yeah, just beat it!????".to_string());
    println!("'{}' in binary = {} and in hex = {}", "hello ", a, b);
    println!("'{}' in binary = {} / {} and in hex = {}", "Lift off! bro what, huh yeah, just beat it!????", c, c.len(), d);
    let e = utility::partitionDocument(c, x.len().try_into().unwrap());
    let f = utility::partitionMessage(d, x.len().try_into().unwrap());
    println!("grouped msg = {:?}", e);
    println!("grouped hex msg = {:?}", f);
    println!("shuffled hex first word = {:?}", utility::shuffleVector(f[0][0].clone()));
    let (row, col) = utility::formatIndex(f[0][0][0].clone());
    println!("aes sub row / column = {} / {}", row, col);
    println!("from constant s(90, 08) = {}", utility::constants::sBox.get(&("90", "08")).unwrap());
    println!("from constant i-s(90, 08) = {}", utility::constants::inverseSubstitution.get(&("90", "08")).unwrap());

    println!("from constant mix@2 = {:?}", utility::constants::mixingMatrix[2]);
    println!("from constant i-mix@2 = {:?}", utility::constants::inverseMatrix[2]);

}
