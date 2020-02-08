#!/bin/bash
commit () {
	local git_dir="${GS_GIT_DIR}"
	
	cd $git_dir
	cp "$tmp_dir/$db_name" .
	cp "$tmp_dir/$db_name.sql" .
	git commit -am "$1"
	git push
}

extract () {
	#db=`unzip -Z -1 "${1}"`
	unzip "${1}" -d $tmp_dir;
}

dump () {
	local out_db="$tmp_dir/plaintext.db"
	local key="harada-san"

	echo "PRAGMA key='$key';PRAGMA cipher_compatibility = 3;ATTACH DATABASE '$out_db' AS plaintext KEY '';SELECT sqlcipher_export('plaintext');DETACH DATABASE plaintext" | sqlcipher "$tmp_dir/$db_name";
	sqlcipher "$out_db" .dump > "$tmp_dir/$db_name.sql";
	#echo "$tmp_dir/$db" "$tmp_dir/$db.sql" 
	ls -1 "$tmp_dir/$db_name"
	ls -1 "$tmp_dir/$db_name.sql"
	rm -rf $out_db;

}

download_db () {
	wget -P $tmp_dir $1 
}


if [ "$1" != "" ]; then
	tmp_dir=`mktemp -d`
	echo $tmp_dir
	db_name='encrypted_app.db'
	
	version=`echo "$1" | cut -d'_' -f3 | cut -d'.' -f1 | sed 's/^0*//'`
	echo $version

	extract $1
	dump $1
	commit $version
else
	echo "failed"
fi

