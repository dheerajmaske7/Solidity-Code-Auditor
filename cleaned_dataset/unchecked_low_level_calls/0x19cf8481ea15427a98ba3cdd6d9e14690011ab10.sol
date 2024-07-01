pragma solidity ^0.4.11;
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }
contract MigrationAgent {
    function migrateFrom(address _from, uint256 _value);
}
contract ERC20 {
  uint public totalSupply;
  function balanceOf(address who) constant returns (uint);
  function allowance(address owner, address spender) constant returns (uint);
  function transfer(address to, uint value) returns (bool ok);
  function transferFrom(address from, address to, uint value) returns (bool ok);
  function approve(address spender, uint value) returns (bool ok);
  event Transfer(address indexed from, address indexed to, uint value);
  event Approval(address indexed owner, address indexed spender, uint value);
}
contract SafeMath {
  function safeMul(uint a, uint b) internal returns (uint) {
    uint c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function safeDiv(uint a, uint b) internal returns (uint) {
    assert(b > 0);
    uint c = a / b;
    assert(a == b * c + a % b);
    return c;
  }
  function safeSub(uint a, uint b) internal returns (uint) {
    assert(b <= a);
    return a - b;
  }
  function safeAdd(uint a, uint b) internal returns (uint) {
    uint c = a + b;
    assert(c>=a && c>=b);
    return c;
  }
  function max64(uint64 a, uint64 b) internal constant returns (uint64) {
    return a >= b ? a : b;
  }
  function min64(uint64 a, uint64 b) internal constant returns (uint64) {
    return a < b ? a : b;
  }
  function max256(uint256 a, uint256 b) internal constant returns (uint256) {
    return a >= b ? a : b;
  }
  function min256(uint256 a, uint256 b) internal constant returns (uint256) {
    return a < b ? a : b;
  }
  function assert(bool assertion) internal {
    if (!assertion) {
      throw;
    }
  }
}
contract StandardToken is ERC20, SafeMath {
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    function burn(uint256 _value) public returns (bool success) {
        require(balances[msg.sender] >= _value);   
        balances[msg.sender] -= _value;            
        totalSupply -= _value;                      
        Burn(msg.sender, _value);
        return true;
    }
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balances[_from] >= _value);                
        require(_value <= allowed[_from][msg.sender]);    
        balances[_from] -= _value;                         
        allowed[_from][msg.sender] -= _value;             
        totalSupply -= _value;                              
        Burn(_from, _value);
        return true;
    }
  function transfer(address _to, uint256 _value) returns (bool success) {
    if (balances[msg.sender] >= _value && balances[_to] + _value > balances[_to]) {
      balances[msg.sender] -= _value;
      balances[_to] += _value;
      Transfer(msg.sender, _to, _value);
      return true;
    } else { return false; }
  }
  function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
    if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && balances[_to] + _value > balances[_to]) {
      balances[_to] += _value;
      balances[_from] -= _value;
      allowed[_from][msg.sender] -= _value;
      Transfer(_from, _to, _value);
      return true;
    } else { return false; }
  }
  function balanceOf(address _owner) constant returns (uint256 balance) {
    return balances[_owner];
  }
  function approve(address _spender, uint256 _value) returns (bool success) {
    allowed[msg.sender][_spender] = _value;
    Approval(msg.sender, _spender, _value);
    return true;
  }
  function allowance(address _owner, address _spender) constant returns (uint256 remaining) {
    return allowed[_owner][_spender];
  }
	    function () payable  public {
		 if(funding){ 
        receivedEther(msg.sender, msg.value);
		balances[msg.sender]=balances[msg.sender]+msg.value;
		} else throw;
    }
  function setTokenInformation(string _name, string _symbol) {
	   if (msg.sender != owner) {
      throw;
    }
	name = _name;
    symbol = _symbol;
    UpdatedTokenInformation(name, symbol);
  }
function setChainsAddresses(address chainAd, int chainnumber) {
	   if (msg.sender != owner) {
      throw;
    }
	if(chainnumber==1){Chain1=chainAd;}
	if(chainnumber==2){Chain2=chainAd;}
	if(chainnumber==3){Chain3=chainAd;}
	if(chainnumber==4){Chain4=chainAd;}		
  } 
  function DAOPolskaTokenICOregulations() external returns(string wow) {
	return 'Regulations of preICO and ICO are present at website  DAO Polska Token.network and by using this smartcontract and blockchains you commit that you accept and will follow those rules';
}
	function sendTokenAw(address StandardTokenAddress, address receiver, uint amount){
		if (msg.sender != owner) {
		throw;
		}
		sendTokenAway t = transfers[numTransfers];
		t.coinContract = StandardToken(StandardTokenAddress);
		t.amount = amount;
		t.recipient = receiver;
		t.coinContract.transfer(receiver, amount);
		numTransfers++;
	}
uint public tokenCreationRate=1000;
uint public bonusCreationRate=1000;
uint public CreationRate=1761;
   uint256 public constant oneweek = 36000;
uint256 public fundingEndBlock = 5433616;
bool public funding = true;
bool public refundstate = false;
bool public migratestate= false;
        function createDaoPOLSKAtokens(address holder) payable {
        if (!funding) throw;
        if (msg.value == 0) throw;
        if (msg.value > (supplylimit - totalSupply) / CreationRate)
          throw;
	 var numTokensRAW = msg.value;
        var numTokens = msg.value * CreationRate;
        totalSupply += numTokens;
        balances[holder] += numTokens;
        balancesRAW[holder] += numTokensRAW;
        Transfer(0, holder, numTokens);
        uint256 percentOfTotal = 12;
        uint256 additionalTokens = 	numTokens * percentOfTotal / (100);
        totalSupply += additionalTokens;
        balances[migrationMaster] += additionalTokens;
        Transfer(0, migrationMaster, additionalTokens);
	}
	function setBonusCreationRate(uint newRate){
	if(msg.sender == owner) {
	bonusCreationRate=newRate;
	CreationRate=tokenCreationRate+bonusCreationRate;
	}
	}
    function FundsTransfer() external {
	if(funding==true) throw;
		 	if (!owner.send(this.balance)) throw;
    }
    function PartialFundsTransfer(uint SubX) external {
	      if (msg.sender != owner) throw;
        owner.send(this.balance - SubX);
	}
	function turnrefund() external {
	      if (msg.sender != owner) throw;
	refundstate=!refundstate;
        }
			function fundingState() external {
	      if (msg.sender != owner) throw;
	funding=!funding;
        }
    function turnmigrate() external {
	      if (msg.sender != migrationMaster) throw;
	migratestate=!migratestate;
}
function finalize() external {
        if (block.number <= fundingEndBlock+8*oneweek) throw;
        funding = false;	
		refundstate=!refundstate;
        if (msg.sender==owner)
		owner.send(this.balance);
    }
    function migrate(uint256 _value) external {
        if (migratestate) throw;
        if (_value == 0) throw;
        if (_value > balances[msg.sender]) throw;
        balances[msg.sender] -= _value;
        totalSupply -= _value;
        totalMigrated += _value;
        MigrationAgent(migrationAgent).migrateFrom(msg.sender, _value);
        Migrate(msg.sender, migrationAgent, _value);
    }
function refundTRA() external {
        if (funding) throw;
        if (!refundstate) throw;
        var DAOPLTokenValue = balances[msg.sender];
        var ETHValue = balancesRAW[msg.sender];
        if (ETHValue == 0) throw;
        balancesRAW[msg.sender] = 0;
        totalSupply -= DAOPLTokenValue;
        Refund(msg.sender, ETHValue);
        msg.sender.transfer(ETHValue);
}
function preICOregulations() external returns(string wow) {
	return 'Regulations of preICO are present at website  daopolska.pl and by using this smartcontract you commit that you accept and will follow those rules';
}
}