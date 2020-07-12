<?php
// need data in cookie
/**
a xor b = c
c xor a = a xor b xor a = a xor a xor b = b

plaintext xor key = ciphertext
ciphertext xor plaintext = key

plaintext is json_encode array( "showpassword"=>"no", "bgcolor"=>"#ffffff")
ciphertext is base64_decode ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%3D
**/
function xor_encrypt() {
    $plaintext=json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff"));
    $ciphertext=base64_decode('ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%3D');
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($plaintext);$i++) {
    $outText .= $plaintext[$i] ^ $ciphertext[$i];
    }

    return $outText;
}
echo xor_encrypt();
?>
