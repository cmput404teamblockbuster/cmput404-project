module.exports={
  extract: function (url) {
      const array = url.split('/');
      return array[array.length-1]
  }  
};