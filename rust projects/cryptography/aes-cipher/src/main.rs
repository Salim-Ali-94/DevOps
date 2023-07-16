mod utility;


fn main() {

    let msg = "Lift off".to_string();
    let aes_standard = 128;
    let (binary_key, hex_key_matrix, rounds) = utility::aesKeyGenerator(aes_standard);
    println!("\n\nthe aes key is = {} / {}-bits\n\n", binary_key, binary_key.len());
    println!("stacked hex key is = {:?} / {}-rows\n\n", hex_key_matrix, hex_key_matrix.len());
    println!("#rounds = {}\n\n", rounds);
    let (encoded_doc, hex_msg_matrix) = utility::spliceDocument(msg.clone(), binary_key.len().try_into().unwrap());
    // println!("'{}' in binary = {} and the hex-matrix = {:?}", msg, encoded_doc, hex_msg_matrix);
    println!("'{}' in hex = {} / {}-chars and the hex-matrix = {:?}\n\n", msg, encoded_doc, encoded_doc.len(), hex_msg_matrix);
    // let doc = utility::scrambleDocument(hex_msg_matrix, hex_key_matrix);
    // println!("doc = {:?}\n\n", doc);
    // utility::scrambleDocument(hex_msg_matrix, hex_key_matrix);
    utility::scrambleDocument(hex_msg_matrix, hex_key_matrix, rounds);

    // let encrypted_document = utility::scrambleDocument(aes_standard, msg);

    // println!("shuffled hex first word = {:?}", utility::shuffleVector(f[0][0].clone()));
    // let (row, col) = utility::formatIndex(f[0][0][0].clone());
    // println!("aes sub row / column = {} / {}", row, col);
    // println!("from constant s(90, 08) = {}", utility::constants::sBox.get(&("90", "08")).unwrap());
    // println!("from constant i-s(90, 08) = {}", utility::constants::inverseSubstitution.get(&("90", "08")).unwrap());
    // println!("from constant mix@2 = {:?}", utility::constants::mixingMatrix[2]);
    // println!("from constant i-mix@2 = {:?}", utility::constants::inverseMatrix[2]);

}
