module.exports={
  extract: function (url) {
      const array = url.split('/');
      const index = array[array.length-1] === ""? array.length-2:array.length-1;
      return array[index]
  }  
};