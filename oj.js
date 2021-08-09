//1
while(line = readline()){
    let arr = line.split(' ');
    console.log(parseInt(arr[0])+parseInt(arr[1]));
}
//2
let count = 0;
while(line = readline()){
    if(count === 0){
        count++;
    }else{
        let arr = line.split(' ');
        console.log(parseInt(arr[0])+parseInt(arr[1]));
    }
}
//3
while(line = readline()){
    let arr = line.split(' ');
    if(parseInt(arr[0])!==0){
        console.log(parseInt(arr[0]) + parseInt(arr[1]));
    }
}
//4
while(line = readline()){
    let arr = line.split(' ');
    if(parseInt(arr[0])!==0){
        let arrCopy = [...arr.slice(1)];
        console.log(arrCopy.reduce((pre, cur)=>{
            return parseInt(pre) + parseInt(cur);
        }))
    }
}
//5
let count = 0;
while(line = readline()){
    if(count === 0){
        count++;
    }else{
        let arr = line.split(' ');
        let arrCopy = [...arr.slice(1)];
        console.log(arrCopy.reduce((pre, cur)=>{
            return parseInt(pre) + parseInt(cur);
        }))
    }    
}
//6
while(line = readline()){
    let arr = line.split(' ');
    let arrCopy = [...arr.slice(1)];
    console.log(arrCopy.reduce((pre, cur)=>{
        return parseInt(pre) + parseInt(cur);
    }))
}
//7
while(line = readline()){
    let arr = line.split(' ');
    console.log(arr.reduce((pre, cur)=>{
        return parseInt(pre) + parseInt(cur);
    }))
}
//8
let count = 0;
while(line = readline()){
    if(count === 0){
        count++;
    }else{
        let arr = line.split(' ');
        arr.sort((a,b)=>{
            return a>b?1:a<b?-1:0;
        })
        console.log(arr.join(' '));
    }    
}
//9
while(line = readline()){
    let arr = line.split(' ');
    arr.sort((a,b)=>{
        return a>b?1:a<b?-1:0;
    })
    console.log(arr.join(' '));
}
//10
while(line = readline()){
    let arr = line.split(',');
    arr.sort((a,b)=>{
        return a>b?1:a<b?-1:0;
    })
    console.log(arr.join(','));
}
//11
while(line = readline()){
    let arr = line.split(' ');
    console.log(parseInt(arr[0]) + parseInt(arr[1]));
}